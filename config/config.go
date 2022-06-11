package main

import (
	"fmt"
	"io/ioutil"

	"gopkg.in/yaml.v3"
)

type Config struct {
	Port          int    `yaml:"port"`
	Adress_server string `yaml:"address_server"`
	Hostname      string `yaml:"hostname"`
	Start_html    string `yaml:"start-html"`
	Web_directory string `yaml:"web-directory"`
}

func (c *Config) Parse(content []byte) error {
	return yaml.Unmarshal(content, c)
}

func main() {
	name_config := "config.yml"
	fmt.Println("Wczytywanie plik konfiguracyjnego: ", name_config)
	content, err := ioutil.ReadFile(name_config)
	if err != nil {
		fmt.Println("Nie udalo sie odczytac zawartosc pliku ", name_config)
	}
	var config Config
	if err := config.Parse(content); err != nil {
		fmt.Println(err)
	}
	fmt.Println("Zawartosc konfiguracji: \n")
	fmt.Printf("Port = %d\n", config.Port)
	fmt.Printf("Hostname = %s\n", config.Hostname)
	fmt.Printf("Address server = %s\n", config.Adress_server)
	fmt.Printf("Start-html = %s\n", config.Start_html)
	fmt.Printf("Web-directory = %s\n\n", config.Web_directory)
	fmt.Printf("Wczytywanie pliku %s zakonczona", name_config)
}
