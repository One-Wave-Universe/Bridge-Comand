package org.onewave.relay
import android.app.*
import android.content.Intent
import android.os.IBinder
import androidx.core.app.NotificationCompat
class BridgeService: Service() {
 companion object { const val CHANNEL="one_wave_bridge"; const val NOTIFICATION=4101 }
 override fun onCreate(){ super.onCreate(); createChannel(); startForeground(NOTIFICATION, notification("AI Hub running — bridge doctor active")); HubPrefs(this).setRunning(true) }
 override fun onStartCommand(intent:Intent?,flags:Int,startId:Int):Int { HubPrefs(this).touchHealthy(); return START_STICKY }
 override fun onDestroy(){ HubPrefs(this).setRunning(false); super.onDestroy() }
 override fun onBind(intent:Intent?):IBinder?=null
 private fun createChannel(){ if(android.os.Build.VERSION.SDK_INT>=26) (getSystemService(NotificationManager::class.java)).createNotificationChannel(NotificationChannel(CHANNEL,"One-Wave AI Hub",NotificationManager.IMPORTANCE_LOW)) }
 private fun notification(text:String)=NotificationCompat.Builder(this,CHANNEL).setSmallIcon(android.R.drawable.stat_notify_sync_noanim).setContentTitle("One-Wave AI Hub").setContentText(text).setOngoing(true).build()
}
