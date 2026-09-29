package org.onewave.relay
import android.content.Context
import android.content.Intent
import androidx.core.content.ContextCompat
import androidx.work.Worker
import androidx.work.WorkerParameters
class BridgeDoctorWorker(c:Context,p:WorkerParameters):Worker(c,p){
 override fun doWork():Result{
  val prefs=HubPrefs(applicationContext)
  if(!prefs.enabled()) return Result.success()
  return try {
   ContextCompat.startForegroundService(applicationContext,Intent(applicationContext,BridgeService::class.java))
   prefs.touchHealthy(); Result.success()
  } catch(e:Exception){ Result.retry() }
 }
}
