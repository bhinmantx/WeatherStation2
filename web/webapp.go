package web

import (
	"github.com/labstack/echo/v4"
	"github.com/labstack/echo/v4/middleware"
)

type WebApp struct {
	e   *echo.Echo
	env string
	//db               *gopherneo.Connection
	//auth0
	//commands
}

func New(env string) *WebApp {
	webapp := &WebApp{}
	e := echo.New()
	e.Use(middleware.Logger())
	e.Use(middleware.Recover())

	WireupRoutes(e, webapp)

	webapp.e = e
	return webapp
}

func (w WebApp) Start(httpPort string) {
	w.e.Logger.Fatal(w.e.Start(":" + httpPort))
}
