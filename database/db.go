package database

import (
	"Todo_lister/models"

	"gorm.io/driver/sqlite"
	"gorm.io/gorm"
)

var DB *gorm.DB

func Init() {
	var err error
	DB, err = gorm.Open(sqlite.Open("todo.db"), &gorm.Config{})
	if err != nil {
		panic("failed to connect to database")
	}

	err = DB.AutoMigrate(&models.Todo{})
	if err != nil {
		panic("failed to migrate database")
	}
}
