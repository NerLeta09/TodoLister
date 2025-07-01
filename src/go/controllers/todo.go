package controllers

import (
	"Todo_lister/database"
	"Todo_lister/models"
	"net/http"

	"github.com/gin-gonic/gin"
)

func GetTodos(c *gin.Context) {
	// Fetch all todos from the database
	var todos []models.Todo
	if err := database.DB.Find(&todos).Error; err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to fetch todos"})
		return
	}
	c.JSON(http.StatusOK, todos)

}

func CreateTodo(c *gin.Context) {
	var todo models.Todo
	if err := c.ShouldBindJSON(&todo); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid input"})
		return
	}
}

func ToggleTodo(c *gin.Context) {
	id := c.Param("id")
	var todo models.Todo
	database.DB.First(&todo, id)
	todo.Completed = !todo.Completed
	database.DB.Save(&todo)
	c.JSON(http.StatusOK, todo)
}

func DeleteTodo(c *gin.Context) {
	id := c.Param("id")
	database.DB.Delete(&models.Todo{}, id)
	c.Status(http.StatusNoContent)
}
