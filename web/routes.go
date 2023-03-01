package web

import (
	"net/http"

	"github.com/labstack/echo/v4"
)

func WireupRoutes(e *echo.Echo, webapp *WebApp) {

	e.File("/", "web/assets/index.html")
	e.GET("/ping", func(c echo.Context) error {
		return c.JSON(http.StatusOK, struct{ Status string }{Status: "OK"})
	})
	e.PUT("/command", webapp.command(e))
}

//func(c echo.Context) error {
//	return c.JSON(http.StatusOK, struct{ Status string }{Status: "COMMAND"})
//	}
