package org.onewave.relay

import android.app.Activity
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

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        val root = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setPadding(28,28,28,28)
        }
        idBox = field("Request ID")
        refBox = field("GitHub reference URL")
        bodyBox = field("Question / returned response", true)
        status = TextView(this)
        val send = Button(this).apply { text = "ASK GEMINI / SHARE REQUEST"; setOnClickListener { shareRequest() } }
        val verify = Button(this).apply { text = "VERIFY RETURN"; setOnClickListener { verifyReturn() } }
        val shareReceipt = Button(this).apply { text = "SHARE VERIFIED RECEIPT"; setOnClickListener { shareVerifiedReceipt() } }
        listOf(idBox,refBox,bodyBox,send,verify,shareReceipt,status).forEach { root.addView(it) }
        setContentView(ScrollView(this).apply { addView(root) })
        ingest(intent)
    }

    private fun field(hintText:String, multi:Boolean=false)=EditText(this).apply {
        hint=hintText
        inputType = if(multi) InputType.TYPE_CLASS_TEXT or InputType.TYPE_TEXT_FLAG_MULTI_LINE else InputType.TYPE_CLASS_TEXT
        minLines=if(multi) 10 else 1
    }

    override fun onNewIntent(i:Intent){ super.onNewIntent(i); setIntent(i); ingest(i) }

    private fun ingest(i:Intent) {
        if(i.action==Intent.ACTION_SEND && i.type=="text/plain") {
            val t=i.getStringExtra(Intent.EXTRA_TEXT).orEmpty()
            bodyBox.setText(t)
            Regex("REQUEST_ID:\\s*([^\\s]+)").find(t)?.groupValues?.get(1)?.let { idBox.setText(it) }
            status.text="Received shared text. Verify if this is the return."
        }
    }

    private fun shareRequest() {
        val id=idBox.text.toString().trim()
        val ref=refBox.text.toString().trim()
        val q=bodyBox.text.toString().trim()
        if(id.isEmpty()||ref.isEmpty()||q.isEmpty()){ status.text="HOLD: ID, reference, and question are required."; return }
        val envelope="""ONE-WAVE RELAY one-wave-phone-ai-relay/v1
REQUEST_ID: $id
SOURCE: chatgpt
TARGET: gemini
REFERENCE (inspect before answering):
$ref

QUESTION:
$q

RETURN RULE: Start your reply with exactly REQUEST_ID: $id then give your answer."""
        getSharedPreferences("relay",MODE_PRIVATE).edit().putString("id",id).putString("ref",ref).putString("request",envelope).apply()
        startActivity(Intent.createChooser(Intent(Intent.ACTION_SEND).apply {
            type="text/plain"; putExtra(Intent.EXTRA_TEXT,envelope)
        },"Send request to Gemini"))
    }

    private fun verifyReturn() {
        val expected=getSharedPreferences("relay",MODE_PRIVATE).getString("id","").orEmpty()
        val response=bodyBox.text.toString()
        if(expected.isEmpty()){ status.text="HOLD: no stored request."; return }
        if(!response.contains("REQUEST_ID: $expected")){ status.text="HOLD: response ID does not match $expected"; return }
        status.text="RESPONSE VERIFIED: $expected"
    }

    private fun shareVerifiedReceipt() {
        val p=getSharedPreferences("relay",MODE_PRIVATE)
        val id=p.getString("id","").orEmpty()
        val ref=p.getString("ref","").orEmpty()
        val response=bodyBox.text.toString()
        if(id.isEmpty()||!response.contains("REQUEST_ID: $id")){ status.text="HOLD: verify matching response first."; return }
        val sha=MessageDigest.getInstance("SHA-256").digest(response.toByteArray()).joinToString(""){"%02x".format(it)}
        val receipt=JSONObject().put("schema","one-wave-phone-ai-relay/v1").put("state","RESPONSE")
            .put("id",id).put("source","gemini").put("target","chatgpt").put("reference",ref)
            .put("response",response).put("response_sha256",sha).put("ok",true).toString(2)
        startActivity(Intent.createChooser(Intent(Intent.ACTION_SEND).apply {
            type="text/plain"; putExtra(Intent.EXTRA_TEXT,receipt)
        },"Return verified receipt"))
    }
}
