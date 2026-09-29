package org.onewave.relay

import org.json.JSONObject
import java.net.HttpURLConnection
import java.net.URL

class GeminiClient(private val vault: SecretVault) {
    fun generate(requestId: String, reference: String, message: String): String {
        val key = vault.get("GEMINI_API_KEY") ?: error("GEMINI_API_KEY is not set")
        val prompt = """REQUEST_ID: $requestId
REFERENCE: $reference

Read the supplied reference when it is reachable, then answer the request below.
Start your response with exactly:
REQUEST_ID: $requestId

REQUEST:
$message"""
        val body = JSONObject().put(
            "contents",
            org.json.JSONArray().put(
                JSONObject().put(
                    "parts",
                    org.json.JSONArray().put(JSONObject().put("text", prompt))
                )
            )
        )
        val conn = URL("https://generativelanguage.googleapis.com/v1beta/models/gemini-3.8-flash:generateContent")
            .openConnection() as HttpURLConnection
        conn.requestMethod = "POST"
        conn.connectTimeout = 20000
        conn.readTimeout = 120000
        conn.setRequestProperty("Content-Type", "application/json")
        conn.setRequestProperty("x-goog-api-key", key)
        conn.doOutput = true
        conn.outputStream.use { it.write(body.toString().toByteArray(Charsets.UTF_8)) }
        val code = conn.responseCode
        val stream = if (code in 200..299) conn.inputStream else conn.errorStream
        val raw = stream.bufferedReader().use { it.readText() }
        if (code !in 200..299) error("Gemini HTTP $code: $raw")
        val json = JSONObject(raw)
        val parts = json.getJSONArray("candidates").getJSONObject(0)
            .getJSONObject("content").getJSONArray("parts")
        val text = buildString {
            for (i in 0 until parts.length()) {
                val p = parts.getJSONObject(i)
                if (p.has("text")) append(p.getString("text"))
            }
        }.trim()
        require(text.trimStart().startsWith("REQUEST_ID: $requestId")) {
            "Gemini response/request ID mismatch"
        }
        return text
    }
}
