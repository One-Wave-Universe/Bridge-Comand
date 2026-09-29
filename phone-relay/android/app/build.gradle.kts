plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
}
android {
    namespace = "org.onewave.relay"
    compileSdk = 35
    defaultConfig {
        applicationId = "org.onewave.aihub"
        minSdk = 26
        targetSdk = 35
        versionCode = 5
        versionName = "0.4.1"
    }
    compileOptions { sourceCompatibility = JavaVersion.VERSION_17; targetCompatibility = JavaVersion.VERSION_17 }
    kotlinOptions { jvmTarget = "17" }
}
dependencies {
    implementation("androidx.security:security-crypto:1.1.0-alpha06")
    implementation("androidx.work:work-runtime-ktx:2.10.1")
}
