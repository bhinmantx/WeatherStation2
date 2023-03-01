package main

import (
	"net/http"
	"os"

	Web "github.com/bhinmantx/WeatherStation2/web"
)

func main() {

	httpPort := os.Getenv("HTTP_PORT")
	if httpPort == "" {
		httpPort = "8080"
	}
	webapp := Web.New("local")
	webapp.Start(httpPort)

}
