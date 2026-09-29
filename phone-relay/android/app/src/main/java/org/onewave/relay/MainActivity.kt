package org.onewave.relay

import android.app.Activity
import android.app.AlertDialog
import android.content.Intent
import android.os.Bundle
import android.text.InputType
import android.widget.*
import org.json.JSONObject
import java.security.MessageDigest
import kotlin.concurrent.thread

class MainActivity : Activity() {
    private lateinit var idBox: EditText
    private lateinit var refBox: EditText
    private lateinit var bodyBox: EditText
    private lateinit var status: TextView
    private lateinit var vault: SecretVault
    private lateinit var hub: HubStore

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        vault=SecretVault(this); hub=HubStore(this)
        val root=LinearLayout(this).apply { orientation=LinearLayout.VERTICAL; setPadding(28,28,28,28) }
        root.addView(TextView(this).apply { text="ONE-WAVE COMMUNICATION HUB v0.3" })
        idBox=field("Request ID"); refBox=field("GitHub/reference URL"); bodyBox=field("Message / returned response",true)
        val run=Button(this).apply { text="RUN GEMINI DIRECT"; setOnClickListener { runGemini() } }
        val secrets=Button(this).apply { text="SECRETS VAULT"; setOnClickListener { secretDialog() } }
        val hs=Button(this).apply { text="HUB STATUS"; setOnClickListener { status.text=hub.status().toString(2) } }
        status=TextView(this)
        listOf(idBox,refBox,bodyBox,run,secrets,hs,status).forEach { root.addView(it) }
        setContentView(ScrollView(this).apply { addView(root) }); ingest(intent)
    }
    private fun field(h:String,m:Boolean=false)=EditText(this).apply {
        hint=h; inputType=InputType.TYPE_CLASS_TEXT or if(m) InputType.TYPE_TEXT_FLAG_MULTI_LINE else 0; if(m) minLines=9
    }
    override fun onNewIntent(i:Intent){super.onNewIntent(i);setIntent(i);ingest(i)}
    private fun ingest(i:Intent){
        if(i.action==Intent.ACTION_SEND && i.type=="text/plain"){
            val t=i.getStringExtra(Intent.EXTRA_TEXT).orEmpty(); bodyBox.setText(t)
            Regex("REQUEST_ID:\\s*([^\\s]+)").find(t)?.groupValues?.get(1)?.let{idBox.setText(it)}
            status.text="Inbound request received."
        }
    }
    private fun runGemini(){
        val id=idBox.text.toString().trim()
        val ref=refBox.text.toString().trim()
        val q=bodyBox.text.toString().trim()
        if(id.isEmpty()||ref.isEmpty()||q.isEmpty()){status.text="HOLD: ID, reference, message required";return}
        if(!Regex("[A-Za-z0-9._-]{1,120}").matches(id)){status.text="HOLD: invalid request ID";return}
        status.text="Calling Gemini..."
        hub.write("outbox",id,JSONObject().put("id",id).put("state","REQUEST").put("reference",ref).put("message",q))
        thread {
            try {
                val response=GeminiClient(vault).generate(id,ref,q)
                val sha=MessageDigest.getInstance("SHA-256").digest(response.toByteArray()).joinToString(""){"%02x".format(it)}
                val receipt=JSONObject().put("schema","one-wave-phone-ai-relay/v1").put("state","RESPONSE")
                    .put("id",id).put("source","gemini").put("target","chatgpt").put("reference",ref)
                    .put("response",response).put("response_sha256",sha).put("ok",true)
                hub.write("inbox",id,JSONObject().put("id",id).put("state","RESPONSE").put("response",response))
                hub.write("receipts",id,receipt)
                runOnUiThread { bodyBox.setText(response); status.text="RESPONSE VERIFIED: $id" }
            } catch(e:Exception) {
                runOnUiThread { status.text="HOLD: "+(e.message ?: e.javaClass.simpleName) }
            }
        }
    }
    private fun secretDialog(){
        val box=LinearLayout(this).apply{orientation=LinearLayout.VERTICAL}
        val name=EditText(this).apply{hint="Secret name, e.g. GEMINI_API_KEY"}
        val value=EditText(this).apply{hint="Secret value";inputType=InputType.TYPE_CLASS_TEXT or InputType.TYPE_TEXT_VARIATION_PASSWORD}
        box.addView(name);box.addView(value)
        AlertDialog.Builder(this).setTitle("Encrypted local secrets").setMessage("Stored on this phone only; never written to hub receipts or GitHub.")
            .setView(box).setPositiveButton("SAVE"){_,_->if(name.text.isNotBlank()&&value.text.isNotBlank()){vault.put(name.text.toString(),value.text.toString());status.text="Secret saved locally: "+name.text.toString()}}
            .setNegativeButton("CANCEL",null).show()
    }
}
