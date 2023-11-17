import {
  Streamlit,
  StreamlitComponentBase,
  withStreamlitConnection,
} from "streamlit-component-lib";
import React, { ReactNode } from "react";

const containerStyle: React.CSSProperties = {
  fontFamily: "Source Sans Pro Regular",
  cursor: "pointer",
  marginLeft: "-8px",
  paddingBottom: "4px",
};

const currentPathStyle: React.CSSProperties = {
  fontFamily: "Source Sans Pro Regular",
  cursor: "pointer",
  fontWeight: "bold",
};

interface IPage {
  name: string;
  path: string;
  index: boolean | null;
}

interface LinkProps {
  page: IPage;
  is_last: boolean;
}

function Link({ page, is_last }: LinkProps) {
  function handleClick() {
    if (page.index !== null) {
      if (page.index === false) {
        return;
      }
    }

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
  public render = (): ReactNode => {
    const pages: IPage[] = this.props.args["pages"];

    return (
      <div style={containerStyle}>
        {pages.map((page: IPage, index: number) => (
          <Link key={index} page={page} is_last={index === pages.length - 1} />
        ))}
      </div>
    );
  };
}

export default withStreamlitConnection(Breadcrumbs);
