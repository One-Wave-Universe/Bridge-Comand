package org.onewave.relay
import android.content.Context
import androidx.security.crypto.EncryptedSharedPreferences
import androidx.security.crypto.MasterKey
class SecretVault(context:Context){
 private val master=MasterKey.Builder(context).setKeyScheme(MasterKey.KeyScheme.AES256_GCM).build()
 private val prefs=EncryptedSharedPreferences.create(context,"one_wave_secret_vault",master,EncryptedSharedPreferences.PrefKeyEncryptionScheme.AES256_SIV,EncryptedSharedPreferences.PrefValueEncryptionScheme.AES256_GCM)
 fun put(name:String,value:String)=prefs.edit().putString(name,value).apply()
 fun get(name:String)=prefs.getString(name,null)
 fun names():List<String> = prefs.all.keys.sorted()
 fun remove(name:String)=prefs.edit().remove(name).apply()
}
