import * as React from 'react'
import * as ReactDOM from 'react-dom'



type Handler = () => void

const Button = (props: { label: string, onClick: Handler, disabled?: boolean }) =>
    <button disabled={ props.disabled } onClick={ props.onClick }>{ props.label }</button>



type Position = 'on' | 'off'

class Switch {
    constructor(
        readonly port: number,
        readonly offset: number = 1500,
        readonly position: Position | undefined = undefined
    ) {}
}



interface SwitchControlProps {
    sw: Switch,
    calibrate: (port: number, offset: number) => void
    setPosition: (sw: Switch, position: Position) => void
}

const SwitchControl = ({ sw: { port, offset, position }, calibrate, setPosition }: SwitchControlProps) => {
    const [newOffset, setNewOffset] = React.useState(offset)
    const newPosition = position === 'on' ? 'off' : 'on'
    const buttonLabel = position === 'on' ? 'Off' : 'On'

    return <p>
        Port: { port }
        <input type="number" value={ newOffset } onChange={ e => setNewOffset(parseInt(e.target.value || "0", 10)) } />
        <Button label="Calibrate" onClick={ () => { calibrate(port, newOffset) } } />
        <Button disabled={ position === undefined } label={ buttonLabel } onClick={ () => { setPosition({ port, offset, position }, newPosition) } } />
    </p>
}



const sendCommand = (payload: any): Promise<Position> =>
    fetch('/', { method: 'POST', headers: { 'Content-Type': 'application/json'}, body: JSON.stringify(payload) })
        .then(response => {
            console.log(response)
            return response.statusText === 'Position.ON' ? 'on' : 'off'
        })

const calibrateSwitch = (port: number, offset: number): Promise<Switch> =>
    sendCommand({ port, calibrate: offset }).then(newPosition => new Switch(port, offset, newPosition))

const setSwitchPosition = (sw: Switch, position: Position): Promise<Switch> =>
    sendCommand({ port: sw.port, position }).then(newPosition => new Switch(sw.port, sw.offset, newPosition))



const App = () => {

    const [switches, updateSwitches] = React.useState([new Switch(0, 1360)])

    const addSwitch = () => updateSwitches(values => [...values, new Switch(switches.length)])

    const calibrate = (port: number, offset: number) => calibrateSwitch(port, offset).then(newSwitch =>
        updateSwitches(switches => switches.map(sw => sw.port === newSwitch.port ? newSwitch : sw))
    )

    const setPosition = (sw: Switch, position: Position) => setSwitchPosition(sw, position).then(newSwitch =>
        updateSwitches(switches => switches.map(sw => sw.port === newSwitch.port ? newSwitch : sw))
    )

    return <>
        { switches.map(sw => <SwitchControl key={ sw.port } sw={ sw } calibrate={ calibrate } setPosition={ setPosition } />) }
        <Button label="Add Switch" onClick={ addSwitch } />
        <p>Hello World!</p>
    </>
}


ReactDOM.render(<App />, document.getElementById('app'));
