package web

import (
	"fmt"
	"net/http"

	"github.com/labstack/echo/v4"
)

func WireupRoutes(e *echo.Echo) {

	e.File("/", "web/assets/index.html")
	e.GET("/ping", func(c echo.Context) error {
		return c.JSON(http.StatusOK, struct{ Status string }{Status: "OK"})
	})
	e.POST("/command", func(c echo.Context) error {
		//		AControlFunc(c)
		fmt.Printf("context: %+v", c)
		return c.JSON(http.StatusOK, struct{ Status string }{Status: "COMMAND"})
	})
}
