import { exportComponentAsJPEG, exportComponentAsPDF, exportComponentAsPNG } from 'react-component-export-image';
import React, { MutableRefObject, ReactInstance, useRef, useState } from 'react';
import styled from 'styled-components';


type Role = 'Top' | 'Mid' | 'Bot' 

enum Streamer {
  Bwipo = 'BwipoLoL',
  Lourlo = 'Lourlo',
  Shok = 'Shok',
  Revenge = 'Revenge',
}

enum ChampName {
  Aatrox = 'Aatrox',
  Aphelios = 'Aphelios',
  Samira = 'Samira',
  Zeri = 'Zeri',
  Varus = 'Varus',
  Xayah = 'Xayah',
  Rumble = 'Rumble',
  Pantheon = 'Pantheon',
  Yone = 'Yone',
  Ahri = 'Ahri',
  Kassadin = 'Kassadin',
  Azir = 'Azir',
  Ashe = 'Ashe',
  Jhin = 'Jhin',
  Veigar = 'Veigar',
  Gragas = 'Gragas',
  AurelionSol = 'AurelionSol',
  Gwen = 'Gwen',
};

const FILE_NAME = 9
const VARIANT = 0
const THUMBNAIL_INFO : ThumbnailProps = {
  direction: 'left',
  champName: ChampName.Gwen,
  streamer: Streamer.Revenge
}

type Direction = 'left' | 'right'

interface ThumbnailProps {
  readonly direction: Direction
  readonly champName : ChampName
  readonly streamer: Streamer;
}

const ComponentToPrint = React.forwardRef<ReactInstance, ThumbnailProps>(({direction, champName, streamer}, ref) => {
  console.log(champName)
  const content = <Body champName={champName} direction={direction}>
      <Content direction={direction}>
        <StreamerImage streamerName={streamer}/>
      </Content>
  </Body>
  return React.createElement('div', {ref: ref}, content)
});

const Body = styled.div<{champName : ChampName, direction: Direction}>`
  display: flex;
  width: 1280px;
  height: 720px;
  background-image: linear-gradient(to ${({direction}) => direction}, rgba(0,0,0,0) 0 40%, white 80% 100%), url("${({champName}) => `assets/champs/${champName}_${VARIANT}.jpg`}");
  background-size: 1280px 720px;
  background-repeat: no-repeat;
  justify-content: ${({direction}) => direction === 'left' ? 'flex-start' : 'flex-end'};
`

const Content = styled.div<{direction : Direction}>`
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  align-items: center;
  margin-left: ${({direction}) => direction === 'left' ? '-100px' : 0};
  margin-right: ${({direction}) => direction === 'left' ? 0 : '-100px'};
  `

const SplashArt = styled.div<{champName : ChampName}>`
  background-image: linear-gradient(to right, rgba(0,0,0,0), url(${({champName}) => `assets/champs/${champName}`}));
`

const ChampionImage : React.FC<{champName: ChampName}> = ({champName}) => {
  return <div>
    <SplashArt champName={champName}/>
  </div>
}

const StreamerImage : React.FC<{streamerName: Streamer}> = ({streamerName}) => {

  return <div>
    <img width={800} src={`assets/streamers/${streamerName}.png`}/>
  </div>
}

const MyComponent = () => {
  const componentRef = useRef<ReactInstance>(null);
  const [count, setCount] = useState(0);
  return (
    <React.Fragment>
      <button onClick={() => {
        setCount(count + 1);
        exportComponentAsPNG(componentRef,{
          fileName: FILE_NAME + ""
        });
      }}>
        Export As PNG
      </button>
      <ComponentToPrint ref={componentRef} {...THUMBNAIL_INFO}/>
    </React.Fragment>
  );
};

export default MyComponent;