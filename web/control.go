package web

func (webapp *WebApp) command(c echo.Context) error {
	return c.JSON(http.StatusOK, struct{ Status string }{Status: "COMMAND"})
}
