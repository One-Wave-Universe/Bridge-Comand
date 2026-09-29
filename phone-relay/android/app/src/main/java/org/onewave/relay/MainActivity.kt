package org.onewave.relay

import android.app.Activity
import android.app.AlertDialog
import android.content.Intent
import android.os.Bundle
import android.text.InputType
import android.widget.*
import org.json.JSONObject
import java.security.MessageDigest

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
        root.addView(TextView(this).apply { text="ONE-WAVE COMMUNICATION HUB" })
        idBox=field("Request ID"); refBox=field("GitHub/reference URL"); bodyBox=field("Message / returned response",true)
        val send=Button(this).apply { text="QUEUE + SHARE REQUEST"; setOnClickListener { shareRequest() } }
        val verify=Button(this).apply { text="VERIFY RETURN"; setOnClickListener { verifyReturn() } }
        val receipt=Button(this).apply { text="SHARE VERIFIED RECEIPT"; setOnClickListener { shareReceipt() } }
        val secrets=Button(this).apply { text="SECRETS VAULT"; setOnClickListener { secretDialog() } }
        val hs=Button(this).apply { text="HUB STATUS"; setOnClickListener { status.text=hub.status().toString(2) } }
        status=TextView(this)
        listOf(idBox,refBox,bodyBox,send,verify,receipt,secrets,hs,status).forEach { root.addView(it) }
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
            status.text="Inbound share received."
        }
    }
    private fun shareRequest(){
        val id=idBox.text.toString().trim(); val ref=refBox.text.toString().trim(); val q=bodyBox.text.toString().trim()
        if(id.isEmpty()||ref.isEmpty()||q.isEmpty()){status.text="HOLD: ID, reference, message required";return}
        val envelope="ONE-WAVE RELAY one-wave-phone-ai-relay/v1\nREQUEST_ID: "+id+"\nREFERENCE: "+ref+"\n\nMESSAGE:\n"+q+"\n\nRETURN RULE: Start reply with exactly REQUEST_ID: "+id
        hub.write("outbox",id,JSONObject().put("id",id).put("state","REQUEST").put("reference",ref).put("message",q))
        hub.write("references",id,JSONObject().put("id",id).put("reference",ref))
        getSharedPreferences("relay",MODE_PRIVATE).edit().putString("id",id).putString("ref",ref).apply()
        startActivity(Intent.createChooser(Intent(Intent.ACTION_SEND).apply{type="text/plain";putExtra(Intent.EXTRA_TEXT,envelope)},"Send through hub"))
    }
    private fun verifyReturn(){
        val expected=getSharedPreferences("relay",MODE_PRIVATE).getString("id","").orEmpty(); val response=bodyBox.text.toString()
        if(expected.isEmpty()||!response.contains("REQUEST_ID: "+expected)){status.text="HOLD: response/request ID mismatch";return}
        hub.write("inbox",expected,JSONObject().put("id",expected).put("state","RESPONSE").put("response",response))
        status.text="RESPONSE VERIFIED: "+expected
    }
    private fun shareReceipt(){
        val p=getSharedPreferences("relay",MODE_PRIVATE); val id=p.getString("id","").orEmpty(); val ref=p.getString("ref","").orEmpty(); val response=bodyBox.text.toString()
        if(id.isEmpty()||!response.contains("REQUEST_ID: "+id)){status.text="HOLD: matching response required";return}
        val sha=MessageDigest.getInstance("SHA-256").digest(response.toByteArray()).joinToString(""){"%02x".format(it)}
        val r=JSONObject().put("schema","one-wave-phone-ai-relay/v1").put("state","RESPONSE").put("id",id).put("source","gemini").put("target","chatgpt").put("reference",ref).put("response",response).put("response_sha256",sha).put("ok",true)
        hub.write("receipts",id,r)
        startActivity(Intent.createChooser(Intent(Intent.ACTION_SEND).apply{type="text/plain";putExtra(Intent.EXTRA_TEXT,r.toString(2))},"Return verified receipt"))
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
