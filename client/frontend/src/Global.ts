export class SensorData {
	temperature: number
	humidity: number
	pressure: number
	co2: number
	tvoc: number
	indexLevel: number
	bme280Status: boolean
	ccs811Status: boolean

	constructor(
		temperature: number,
		humidity: number,
		pressure: number,
		co2: number,
		tvoc: number,
		indexLevel: number,
		bme280Status: boolean,
		ccs811Status: boolean

	) {
		this.temperature = temperature
		this.humidity = humidity
		this.pressure = pressure
		this.co2 = co2
		this.tvoc = tvoc
		this.indexLevel = indexLevel
		this.bme280Status = bme280Status
		this.ccs811Status = ccs811Status
	}

	static of(data: any): SensorData {
		return new SensorData(
			data.temperature,
			data.humidity,
			data.pressure,
			data.co2,
			data.tvoc,
			data.indexLevel,
			data.bme280Status,
			data.ccs811Status
		)
	}

	static default() {
		return new SensorData(0, 0, 0, 0, 0, 0, false, false)
	}
}

export class ResponseData {
	hostname: string
	uptime: string
	room: string
	ipAddr: string
	macAddr: string

	alarmEnabled: boolean
	displayEnabled: boolean
	smartAlarmEnabled: boolean
	smartDisplayEnabled: boolean
	displayMode: number
	displayWorking: boolean

	constructor(
		hostname: string,
		uptime: string,
		room: string,
		ipAddr: string,
		macAddr: string,
		alarmEnabled: boolean,
		displayEnabled: boolean,
		smartAlarmEnabled: boolean,
		smartDisplayEnabled: boolean,
		displayMode: number,
		displayWorking: boolean
	) {
		this.hostname = hostname
		this.uptime = uptime
		this.room = room
		this.ipAddr = ipAddr
		this.macAddr = macAddr
		this.alarmEnabled = alarmEnabled
		this.displayEnabled = displayEnabled
		this.smartAlarmEnabled = smartAlarmEnabled
		this.smartDisplayEnabled = smartDisplayEnabled
		this.displayMode = displayMode
		this.displayWorking = displayWorking
	}

	static of(data: any): ResponseData {
		return new ResponseData(
			data.meta.hostname,
			data.meta.uptime,
			data.meta.room,
			data.meta.ipAddr,
			data.meta.macAddr,
			data.controls.alarmEnabled,
			data.controls.displayEnabled,
			data.controls.smartAlarmEnabled,
			data.controls.smartDisplayEnabled,
			data.controls.displayMode,
			data.displayWorking
		)
	}

	static default() {
		return new ResponseData('n.A.', 'n.A.', 'n.A.', 'n.A.', 'n.A.', false, false, false, false, 0, false)
	}
}

export function getUrl() {
	if (process.env.NODE_ENV === 'development') {
		return 'http://localhost:5000'
	}
	return document.location.protocol + '//' + document.location.host
}