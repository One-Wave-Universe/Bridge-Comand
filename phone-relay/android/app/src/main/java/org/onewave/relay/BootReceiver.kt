package org.onewave.relay
import android.content.*
import androidx.work.*
import java.util.concurrent.TimeUnit
class BootReceiver:BroadcastReceiver(){
 override fun onReceive(context:Context,intent:Intent){
  if(!HubPrefs(context).enabled()) return
  val req=PeriodicWorkRequestBuilder<BridgeDoctorWorker>(15,TimeUnit.MINUTES).build()
  WorkManager.getInstance(context).enqueueUniquePeriodicWork("one-wave-bridge-doctor",ExistingPeriodicWorkPolicy.UPDATE,req)
 }
}
