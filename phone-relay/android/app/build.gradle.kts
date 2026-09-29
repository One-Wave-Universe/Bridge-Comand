plugins { id("com.android.application"); id("org.jetbrains.kotlin.android") }
android { namespace="org.onewave.relay"; compileSdk=35
 defaultConfig { applicationId="org.onewave.relay"; minSdk=26; targetSdk=35; versionCode=2; versionName="0.2.0" } }
dependencies { implementation("androidx.security:security-crypto:1.1.0-alpha06") }
