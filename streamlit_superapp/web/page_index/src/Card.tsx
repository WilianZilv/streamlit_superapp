import {
  Streamlit,
  StreamlitComponentBase,
  withStreamlitConnection,
} from "streamlit-component-lib";
import React, { ReactNode } from "react";

export interface IPage {
  name: string;
  icon: string;
  description: string;
  path: string;
  tag: string | null;
  theme: any;
}

interface State {
  hover: boolean;
  count: number;
  isFocused: boolean;
}

const containerStyle: React.CSSProperties = {
  fontFamily: "Source Sans Pro Regular",
  minWidth: "250px",
  maxWidth: "300px",
  flex: 1,
  fontSize: "1.2rem",
  cursor: "pointer",
  padding: "16px",
  borderRadius: "8px",
  userSelect: "none",
  transition: "transform 0.2s ease-in-out",
};

//box-shadow:

// container expand on hover

const descriptionStyle: React.CSSProperties = {
  fontSize: "1rem",
  fontWeight: 200,
  lineHeight: "1.5rem",
};

const gap: React.CSSProperties = {
  height: "8px",
};

/**
 * This is a React-based component template. The `render()` function is called
 * automatically when your component should be re-rendered.
 */

// define props
interface Props {
  page: IPage;
  theme: any;
  onClick: (page: IPage) => void;
}

export default function Page({ page, theme, onClick }: Props) {
  const { name, icon, description }: IPage = page;

  const [hover, setHover] = React.useState(false);

  function onMouseEnter() {
    setHover(true);
  }
  function onMouseLeave() {
    setHover(false);
  }

  function onClicked() {
    onClick(page);
  }

  const transform = hover ? "scale(1.02)" : "scale(1)";

  let backgroundColor = "rgb(26, 28, 36)";
  let color = "white";

  if (theme) {
    backgroundColor =
      theme.base == "dark" ? backgroundColor : theme.secondaryBackgroundColor;
    color = theme.textColor;
  }

  return (
    <div
      onMouseEnter={onMouseEnter}
      onMouseLeave={onMouseLeave}
      style={{ ...containerStyle, backgroundColor, color, transform }}
      onClick={onClicked}
    >
      <span>
        {icon} {name}
      </span>
      <div style={gap}></div>
      {description &&
        description.split("\n").map((line: string, i: number) => (
          <span key={i} style={descriptionStyle}>
            {line}
            <br />
          </span>
        ))}
    </div>
  );
}
