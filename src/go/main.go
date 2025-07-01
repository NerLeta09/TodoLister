package main

import (
	"Todo_lister/database"
	"Todo_lister/routes"

	"github.com/gin-gonic/gin"
)

func main() {
	database.Init()
	r := gin.Default()
	routes.RegisterRoutes(r)
	r.Run(":8000")
}
