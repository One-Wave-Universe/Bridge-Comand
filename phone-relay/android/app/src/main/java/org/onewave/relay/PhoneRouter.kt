package org.onewave.relay
import android.content.Context
import org.json.JSONObject

class PhoneRouter(c:Context,private val vault:SecretVault){
 private val health=RouteHealth(c)
 fun routeIds()=listOf("gemini-direct","github-actions","android-share")
 fun dispatchGitHub(requestId:String,workflow:String,inputs:JSONObject):JSONObject{
  return try{
   val r=GitHubClient(vault).dispatch("One-Wave-Universe","Bridge-Comand",workflow,"main",inputs)
   health.success("github-actions")
   JSONObject().put("schema","one-wave-phone-route/v1").put("id",requestId).put("route","github-actions").put("state","DISPATCHED").put("dispatch",r).put("health",health.json(routeIds()))
  }catch(e:Exception){health.failure("github-actions");throw e}
 }
 fun success(route:String)=health.success(route)
 fun failure(route:String)=health.failure(route)
 fun health()=health.json(routeIds())
 fun preferred()=health.preferred(routeIds())?:"android-share"
}
