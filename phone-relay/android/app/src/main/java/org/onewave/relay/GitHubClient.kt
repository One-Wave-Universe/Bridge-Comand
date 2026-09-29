package org.onewave.relay
import org.json.JSONObject
import java.net.HttpURLConnection
import java.net.URL

class GitHubClient(private val vault:SecretVault){
 private fun call(method:String,url:String,body:JSONObject?=null):Pair<Int,String>{
  val token=vault.get("GITHUB_TOKEN")?:error("GITHUB_TOKEN is not set")
  val c=URL(url).openConnection() as HttpURLConnection
  c.requestMethod=method;c.connectTimeout=20000;c.readTimeout=60000
  c.setRequestProperty("Accept","application/vnd.github+json")
  c.setRequestProperty("Authorization","Bearer $token")
  c.setRequestProperty("X-GitHub-Api-Version","2026-03-10")
  if(body!=null){c.setRequestProperty("Content-Type","application/json");c.doOutput=true;c.outputStream.use{it.write(body.toString().toByteArray())}}
  val code=c.responseCode;val s=if(code in 200..299)c.inputStream else c.errorStream
  return code to (s?.bufferedReader()?.use{it.readText()}.orEmpty())
 }
 fun dispatch(owner:String,repo:String,workflow:String,ref:String,inputs:JSONObject):JSONObject{
  val url="https://api.github.com/repos/$owner/$repo/actions/workflows/$workflow/dispatches"
  val (code,raw)=call("POST",url,JSONObject().put("ref",ref).put("inputs",inputs))
  if(code !in 200..299) error("GitHub dispatch HTTP $code: $raw")
  return if(raw.isBlank()) JSONObject().put("ok",true).put("status",code) else JSONObject(raw).put("ok",true)
 }
 fun get(path:String):JSONObject{
  val (code,raw)=call("GET","https://api.github.com$path")
  if(code !in 200..299) error("GitHub HTTP $code: $raw")
  return JSONObject(raw)
 }
}
