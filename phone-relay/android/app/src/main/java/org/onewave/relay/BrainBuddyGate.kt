package org.onewave.relay
import android.content.Context
import org.json.JSONArray
import org.json.JSONObject
import java.security.MessageDigest

/**
 * HARD Brain Buddy gate for the Android app.
 * Provider calls receive a GatePacket only. A bare user question cannot cross this class.
 */
class BrainBuddyGate(private val context:Context, private val vault:SecretVault){
 data class GatePacket(val requestId:String,val json:String,val sha256:String)
 private val github=GitHubClient(vault)
 private val store=HubStore(context)

 private fun nonBlank(o:JSONObject,key:String):String{
  val v=o.optString(key,"").trim(); if(v.isEmpty()) error("GATE BLOCKED: missing $key"); return v
 }
 private fun sha(s:String)=MessageDigest.getInstance("SHA-256").digest(s.toByteArray()).joinToString(""){"%02x".format(it)}

 fun open(requestId:String, question:String, conversation:JSONArray, repo:JSONObject):GatePacket{
  if(requestId.isBlank()||question.isBlank()) error("GATE BLOCKED: request/question required")
  if(conversation.length()==0) error("GATE BLOCKED: prior/current conversation required")
  val owner=nonBlank(repo,"owner"); val name=nonBlank(repo,"repo"); val ref=nonBlank(repo,"ref")
  val canonical=nonBlank(repo,"canonical_start")
  val paths=repo.optJSONArray("paths")?:JSONArray()
  if(paths.length()==0) error("GATE BLOCKED: relevant repo references required")

  val refs=JSONArray()
  fun fetch(path:String){
   val f=github.readFile(owner,name,path,ref)
   refs.put(JSONObject().put("path",path).put("blob_sha",f.getString("sha")).put("content",f.getString("content")))
  }
  fetch(canonical)
  for(i in 0 until paths.length()){val p=paths.getString(i);if(p!=canonical)fetch(p)}

  val packet=JSONObject()
   .put("brain_buddy",true).put("request_id",requestId).put("question",question)
   .put("conversation",conversation)
   .put("repository",JSONObject().put("owner",owner).put("repo",name).put("ref",ref).put("canonical_start",canonical).put("references",refs))
   .put("gate",JSONObject().put("status","OPEN").put("rule","conversation+repo verified before provider"))
  val raw=packet.toString()
  val digest=sha(raw)
  packet.getJSONObject("gate").put("packet_sha256",digest)
  store.write("references",requestId,packet)
  return GatePacket(requestId,packet.toString(),digest)
 }
}
