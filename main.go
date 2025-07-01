package main

import (
	"log"
	"os"
	"os/exec"
	"os/signal"
	"syscall"

	"Todo_lister/database"
	"Todo_lister/routes"

	"github.com/gin-gonic/gin"
)

func main() {
	database.Init()
	r := gin.Default()
	routes.RegisterRoutes(r)

	cmd := exec.Command("python", "-m", "frontend.panel")

	err := cmd.Start()
	if err != nil {
		log.Fatalf("Failed to start panel.py: %v", err)
	}
	log.Println("panel.py started successfully")

	// 监听 Python 进程退出的 goroutine
	go func() {
		err := cmd.Wait() // 阻塞等待 Python 退出
		if err != nil {
			log.Printf("panel.py exited with error: %v", err)
		} else {
			log.Println("panel.py exited normally")
		}
		// 当 Python UI 退出，优雅停止 Go 服务
		log.Println("Stopping Go server because Python UI closed...")
		// 退出整个程序
		os.Exit(0)
	}()

	// 监听系统中断信号，方便优雅退出
	quit := make(chan os.Signal, 1)
	signal.Notify(quit, os.Interrupt, syscall.SIGTERM)
	go func() {
		<-quit
		log.Println("Received interrupt signal, shutting down...")
		if cmd.Process != nil {
			_ = cmd.Process.Kill() // 关闭Python进程
		}
		os.Exit(0)
	}()

	r.Run(":8000")
}
