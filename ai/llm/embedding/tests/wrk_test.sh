# wrk 用法
# -t 启动多少个线程
# -c HTTP连接总数, 每个线程处理N = 总连接数/线程的个数
# -d 持续时间，例如：2s, 2m, 2h
# -s 指定Lua脚本路径

wrk -t 16 -c 100 -d 60s -s wrk.lua --timeout 10s http://127.0.0.1:5000/embed