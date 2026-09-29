package org.onewave.relay
import android.content.Context
class HubPrefs(c:Context){
 private val p=c.getSharedPreferences("hub_runtime",Context.MODE_PRIVATE)
 fun setEnabled(v:Boolean)=p.edit().putBoolean("enabled",v).apply()
 fun enabled()=p.getBoolean("enabled",false)
 fun setRunning(v:Boolean)=p.edit().putBoolean("running",v).apply()
 fun running()=p.getBoolean("running",false)
 fun touchHealthy()=p.edit().putLong("last_healthy",System.currentTimeMillis()).apply()
 fun lastHealthy()=p.getLong("last_healthy",0)
}
