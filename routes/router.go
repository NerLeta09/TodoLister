package routes

import (
	"Todo_lister/controllers"

	"github.com/gin-gonic/gin"
)

func RegisterRoutes(router *gin.Engine) {
	router.GET("/todos", controllers.GetTodos)
	router.POST("/todos", controllers.CreateTodo)
	router.PUT("/todos/:id/toggle", controllers.ToggleTodo)
	router.DELETE("/todos/:id", controllers.DeleteTodo)
}
