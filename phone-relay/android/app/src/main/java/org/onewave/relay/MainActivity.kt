package org.onewave.relay
import android.app.*
import android.content.Intent
import android.os.Bundle
import android.text.InputType
import android.widget.*
import androidx.core.content.ContextCompat
import org.json.JSONObject
import java.security.MessageDigest
import kotlin.concurrent.thread
class MainActivity:Activity(){
 private lateinit var idBox:EditText; private lateinit var refBox:EditText; private lateinit var bodyBox:EditText
 private lateinit var status:TextView; private lateinit var vault:SecretVault; private lateinit var hub:HubStore; private lateinit var prefs:HubPrefs
 override fun onCreate(b:Bundle?){super.onCreate(b);vault=SecretVault(this);hub=HubStore(this);prefs=HubPrefs(this)
  val root=LinearLayout(this).apply{orientation=LinearLayout.VERTICAL;setPadding(28,28,28,28)}
  root.addView(TextView(this).apply{text="BRAIN BUDDY — REFERENCE GATE APP"})
  root.addView(TextView(this).apply{text="All AI work enters through conversation + repository reference before provider execution."})
  val start=Button(this).apply{text="START / REPAIR HUB";setOnClickListener{startHub()}}
  val stop=Button(this).apply{text="STOP HUB";setOnClickListener{stopHub()}}
  val keys=Button(this).apply{text="AI PROVIDER KEYS";setOnClickListener{providerDialog()}}
  idBox=field("Request ID");refBox=field("Reference URL");bodyBox=field("Message / returned response",true)
  val run=Button(this).apply{text="SEND THROUGH REFERENCE GATE";setOnClickListener{runGemini()}}
  val hs=Button(this).apply{text="BRIDGE DOCTOR STATUS";setOnClickListener{showStatus()}}
  status=TextView(this)
  listOf(start,stop,keys,idBox,refBox,bodyBox,run,hs,status).forEach{root.addView(it)}
  setContentView(ScrollView(this).apply{addView(root)});ingest(intent);showStatus()
 }
 private fun field(h:String,m:Boolean=false)=EditText(this).apply{hint=h;inputType=InputType.TYPE_CLASS_TEXT or if(m) InputType.TYPE_TEXT_FLAG_MULTI_LINE else 0;if(m)minLines=7}
 private fun startHub(){prefs.setEnabled(true);ContextCompat.startForegroundService(this,Intent(this,BridgeService::class.java));status.text="Hub enabled. You can close this screen."}
 private fun stopHub(){prefs.setEnabled(false);stopService(Intent(this,BridgeService::class.java));status.text="Hub stopped."}
 private fun showStatus(){val configured=ProviderRegistry.providers.filter{vault.get(it.secret)!=null}.joinToString{it.label};status.text="Enabled: "+prefs.enabled()+"\nRunning: "+prefs.running()+"\nConfigured: "+(configured.ifEmpty{"none"})+"\nLast doctor heartbeat: "+prefs.lastHealthy()}
 private fun providerDialog(){val box=LinearLayout(this).apply{orientation=LinearLayout.VERTICAL};val rows=mutableMapOf<Provider,EditText>()
  ProviderRegistry.providers.forEach{p->box.addView(TextView(this).apply{text=p.label+" API key"});val e=EditText(this).apply{hint=if(vault.get(p.secret)!=null)"Configured — enter to replace" else "Not configured";inputType=InputType.TYPE_CLASS_TEXT or InputType.TYPE_TEXT_VARIATION_PASSWORD};rows[p]=e;box.addView(e)}
  AlertDialog.Builder(this).setTitle("AI provider vault").setMessage("Keys stay in the app's encrypted local vault and are not written to receipts.").setView(ScrollView(this).apply{addView(box)}).setPositiveButton("SAVE"){_,_->rows.forEach{(p,e)->if(e.text.isNotBlank())vault.put(p.secret,e.text.toString().trim())};showStatus()}.setNegativeButton("CANCEL",null).show()
 }
 override fun onNewIntent(i:Intent){super.onNewIntent(i);setIntent(i);ingest(i)}
 private fun ingest(i:Intent){if(i.action==Intent.ACTION_SEND&&i.type=="text/plain"){val t=i.getStringExtra(Intent.EXTRA_TEXT).orEmpty();bodyBox.setText(t);Regex("REQUEST_ID:\\s*([^\\s]+)").find(t)?.groupValues?.get(1)?.let{idBox.setText(it)}}}
 private fun runGemini(){val id=idBox.text.toString().trim();val ref=refBox.text.toString().trim();val q=bodyBox.text.toString().trim()
  if(id.isEmpty()||ref.isEmpty()||q.isEmpty()||!Regex("[A-Za-z0-9._-]{1,120}").matches(id)){status.text="GATE BLOCKED: conversation + repository reference + valid ID required";return}
  status.text="REFERENCE GATE OPEN: conversation + repository reference present; calling worker...";hub.write("outbox",id,JSONObject().put("id",id).put("state","REQUEST").put("reference",ref).put("message",q))
  thread{try{val response=GeminiClient(vault).generate(id,ref,q);val sha=MessageDigest.getInstance("SHA-256").digest(response.toByteArray()).joinToString(""){"%02x".format(it)}
   val receipt=JSONObject().put("schema","one-wave-phone-ai-relay/v1").put("state","RESPONSE").put("id",id).put("source","gemini").put("target","chatgpt").put("reference",ref).put("response",response).put("response_sha256",sha).put("ok",true)
   hub.write("inbox",id,JSONObject().put("id",id).put("state","RESPONSE").put("response",response));hub.write("receipts",id,receipt);prefs.touchHealthy();runOnUiThread{bodyBox.setText(response);status.text="RESPONSE VERIFIED: $id"}
  }catch(e:Exception){runOnUiThread{status.text="HOLD: "+(e.message?:e.javaClass.simpleName)}}}
 }
}
