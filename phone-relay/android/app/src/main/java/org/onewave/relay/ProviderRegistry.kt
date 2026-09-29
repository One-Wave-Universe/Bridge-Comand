package org.onewave.relay
data class Provider(val id:String,val label:String,val secret:String,val model:String)
object ProviderRegistry {
 val providers=listOf(
  Provider("gemini","Gemini","GEMINI_API_KEY","gemini-3.8-flash"),
  Provider("openai","OpenAI","OPENAI_API_KEY",""),
  Provider("anthropic","Claude","ANTHROPIC_API_KEY",""),
  Provider("xai","Grok","XAI_API_KEY",""),
  Provider("deepseek","DeepSeek","DEEPSEEK_API_KEY",""),
  Provider("github","GitHub control lane","GITHUB_TOKEN","")
 )
}
