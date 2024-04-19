-- File: wrk.lua

-- 设置Content-Type为application/json
wrk.headers["Content-Type"] = "application/json"

-- 读取JSON文件内容
local json_file = "data.json"
local json_data = nil
local file = io.open(json_file, "r")
if file then
    json_data = file:read("*a")
    file:close()
else
    print("Failed to open the JSON file")
    os.exit(1)
end

-- 定义wrk任务
wrk.method = "POST"
wrk.body = json_data

-- 可选：用于记录请求和响应信息
function wrk.done(summary, latency, requests)
    print("Requests per second: " .. (summary.requests / summary.duration) * 1000000)
end
