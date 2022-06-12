package main

import (
	"fmt"
	"log"
	"net/http"
)

func main() {
	//	fmt.Fprintln(config.Config.Port)
	http.HandleFunc("./", Simple_Server)
	log.Printf("server is listening at :8080 ..")
	http.ListenAndServe(":8080", nil)
}

func Simple_Server(res http.ResponseWriter, req *http.Request) {
	//title := req.URL.Path[len("/resources/")]
	//p, err := loadPage(title)
	fmt.Fprintf(res, "fff %s", req.URL.Path[1:])
	//t, _ := template.ParseFiles("./resources/index.html")
	//#t.Execute(w, p)

}
