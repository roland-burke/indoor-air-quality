# indoor-air-quality

## Project setup
```
npm install
```

### Compiles and hot-reloads for development
```
npm run serve
```

### Compiles and minifies for production
```
npm run build
```

### Lints and fixes files
```
npm run lint
```
## Connections

The used protocol for communicating with the display is SPI.

	Display - RaspberryPi

	GND  -->  GND
	VDD  -->  3v3
	SCK  -->  SPI_CLK (GPIO 11)
	SDA  -->  SPI_MOSI (GPIO 10)
	RES  -->  GPIO 19
	DC   -->  GPIO 13
	CS   -->  SPI_CE0_N (GPIO 08)
	
	LDR - RaspberryPi
	A    -->  3v3
	B    -->  GPIO 4
	B    -->  GND (with 15.1K resistance)
	
