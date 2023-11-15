import {
  Streamlit,
  StreamlitComponentBase,
  withStreamlitConnection,
} from "streamlit-component-lib";
import React, { ReactNode } from "react";

const containerStyle: React.CSSProperties = {
  fontFamily: "Source Sans Pro Regular",
  cursor: "pointer",
  height: "100%",
  marginBottom: "24px",
};

const currentPathStyle: React.CSSProperties = {
  fontFamily: "Source Sans Pro Regular",
  cursor: "pointer",
  fontWeight: "bold",
};

interface LinkProps {
  page: any;
  is_last: boolean;
}

function Link({ page, is_last }: LinkProps) {
  function handleClick() {
    if (page.index !== null) {
      if (page.index === false) {
        return;
      }
    }

    console.log(page);

    Streamlit.setComponentValue(page.path);
  }

  const step = !is_last ? " / " : "";

  const style = is_last ? currentPathStyle : {};

  return (
    <span style={style} onClick={handleClick}>
      {page.name}
      {step}
    </span>
  );
}

class Breadcrumbs extends StreamlitComponentBase {
  private handleClick = (path: string): void => {
    Streamlit.setComponentValue(path);
  };

  public render = (): ReactNode => {
    const pages = this.props.args["pages"];
    const current_path = this.props.args["current_path"];

    console.log(this.props);

    return (
      <div style={containerStyle}>
        {pages.map((page: any, index: number) => (
          <Link page={page} is_last={index === pages.length - 1} />
        ))}
      </div>
    );
  };
}

export default withStreamlitConnection(Breadcrumbs);
