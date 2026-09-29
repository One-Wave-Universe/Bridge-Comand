package org.onewave.relay
import android.content.Context
import org.json.JSONArray
import org.json.JSONObject
import java.io.File
class HubStore(context:Context){
 private val root=File(context.filesDir,"hub").apply{mkdirs()}
 private fun dir(n:String)=File(root,n).apply{mkdirs()}
 fun write(box:String,id:String,obj:JSONObject){File(dir(box),"$id.json").writeText(obj.toString(2))}
 fun list(box:String):JSONArray{val a=JSONArray();dir(box).listFiles()?.sortedByDescending{it.lastModified()}?.forEach{a.put(it.nameWithoutExtension)};return a}
 fun status()=JSONObject().put("inbox",list("inbox")).put("outbox",list("outbox")).put("receipts",list("receipts")).put("references",list("references"))
}
