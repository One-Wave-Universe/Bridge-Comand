package org.onewave.relay
import android.content.Context
import org.json.JSONObject

class RouteHealth(c:Context){
 private val p=c.getSharedPreferences("route_health",Context.MODE_PRIVATE)
 data class State(val score:Int,val failures:Int,val successes:Int)
 fun state(id:String)=State(p.getInt("$id.score",0),p.getInt("$id.fail",0),p.getInt("$id.ok",0))
 fun success(id:String){val s=state(id);p.edit().putInt("$id.score",(s.score+2).coerceAtMost(12)).putInt("$id.ok",s.successes+1).putInt("$id.fail",0).apply()}
 fun failure(id:String){val s=state(id);p.edit().putInt("$id.score",(s.score-3).coerceAtLeast(-12)).putInt("$id.fail",s.failures+1).apply()}
 fun preferred(ids:List<String>)=ids.maxByOrNull{state(it).score}
 fun json(ids:List<String>)=JSONObject().also{o->ids.forEach{id->val s=state(id);o.put(id,JSONObject().put("score",s.score).put("successes",s.successes).put("failures",s.failures))}}
}
