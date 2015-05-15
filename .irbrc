require 'irb/completion'
require 'irb/ext/save-history'
require 'pp'
require 'rubygems'
require 'wirble'

Wirble.init(:skip_prompt => :DEFAULT)
Wirble.colorize

IRB.conf[:AUTO_INDENT] = true      # default: false
IRB.conf[:SAVE_HISTORY] = 100      # default: nil
IRB.conf[:HISTORY_PATH] = File::expand_path("~/.irb_history")
#IRB.conf[:ECHO] = false            # default: nil


#IRB.conf[:BACK_TRACE_LIMIT] = 16
#IRB.conf[:DEBUG_LEVEL] = 1
#IRB.conf[:EVAL_HISTORY] = nil
#IRB.conf[:HISTORY_FILE] = nil
#IRB.conf[:IGNORE_EOF] = false
#IRB.conf[:IGNORE_EOF] = false
#IRB.conf[:IGNORE_SIGINT] = true
#IRB.conf[:IGNORE_SIGINT] = true
#IRB.conf[:INSPECT_MODE] = nil
#IRB.conf[:IRB_NAME] = "irb"
#IRB.conf[:IRB_RC] = nil
#IRB.conf[:MATH_MODE] = false
#IRB.conf[:PROMPT] = {...}
#IRB.conf[:PROMPT_MODE] = :DEFALUT
#IRB.conf[:SINGLE_IRB] = false
#IRB.conf[:USE_LOADER] = false
#IRB.conf[:USE_LOADER] = false
#IRB.conf[:USE_READLINE] = nil
#IRB.conf[:USE_TRACER] = false
#IRB.conf[:USE_TRACER]=false
#IRB.conf[:VERBOSE]=true
