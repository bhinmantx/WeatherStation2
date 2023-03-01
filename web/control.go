package web

import (
	"encoding/json"

	"github.com/labstack/echo/v4"
)

func MotorControlFunction(c echo.Context) error {

	json_map := make(map[string]interface{})
	err := json.NewDecoder(c.Request().Body).Decode(&json_map)

	return err
}
