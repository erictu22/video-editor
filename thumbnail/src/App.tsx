import { exportComponentAsJPEG, exportComponentAsPDF, exportComponentAsPNG } from 'react-component-export-image';
import React, { MutableRefObject, ReactInstance, useRef } from 'react';

interface ThumbnailProps {
  readonly headerText : String;
  readonly items: String[];
  readonly streamer: String;

}

const ComponentToPrint = React.forwardRef<ReactInstance, ThumbnailProps>((thumbnailProps, ref) => {
  const content = <div>
    Hello world
  </div>
  const output = React.createElement('div', {ref: ref, style: {width: 1280, height: 720}, ...thumbnailProps}, content)
  return output
});

const MyComponent = () => {
  const componentRef = useRef<ReactInstance>(null);

  return (
    <React.Fragment>
      <ComponentToPrint ref={componentRef} />
      <button onClick={() => exportComponentAsJPEG(componentRef)}>
        Export As JPEG
      </button>
      <button onClick={() => exportComponentAsPDF(componentRef)}>
        Export As PDF
      </button>
      <button onClick={() => exportComponentAsPNG(componentRef)}>
        Export As PNG
      </button>
    </React.Fragment>
  );
};

export default MyComponent;