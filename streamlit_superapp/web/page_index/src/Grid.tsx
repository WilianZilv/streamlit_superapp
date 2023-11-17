import {
  Streamlit,
  StreamlitComponentBase,
  withStreamlitConnection,
} from "streamlit-component-lib";
import React, { Fragment, ReactNode } from "react";
import Page, { IPage } from "./Card";

const gridStyle: React.CSSProperties = {
  display: "flex",
  flexWrap: "wrap",
  gap: "8px",
};

const tagStyle: React.CSSProperties = {
  fontFamily: "Source Sans Pro Regular",
};

const EMPTY_TAG = "{ZZZ:}🏷️ Untagged";
const TAG_SORT_PATTERN = "{([^}]+):}";

class Grid extends StreamlitComponentBase {
  private handlePageClick = (page: IPage) => {
    Streamlit.setComponentValue(page.path);
  };

  public render = (): ReactNode => {
    const pages: IPage[] = this.props.args["pages"];
    const { theme } = this.props;

    let tags: string[] = [];

    for (const page of pages) {
      let _tag = page.tag || EMPTY_TAG;
      if (!tags.includes(_tag)) tags.push(_tag);
    }

    function key(tag: string | null) {
      if (!tag) {
        tag = EMPTY_TAG;
      }

      let match = tag.match(TAG_SORT_PATTERN);
      if (match === null) {
        return tag;
      }

      return match[1];
    }

    tags = tags.sort((a, b) => key(a).localeCompare(key(b)));

    function resolveTag(tag: string) {
      let match = tag.match(TAG_SORT_PATTERN);
      if (match === null) {
        return tag;
      }

      return tag.replace(match[0], "");
    }

    let groups: any = {};

    for (const tag of tags) {
      groups[resolveTag(tag)] = pages.filter(
        (page) => (page.tag || EMPTY_TAG) === tag
      );
    }

    const render_tags = tags.length > 1;

    return Object.keys(groups).map((tag) => {
      return (
        <Fragment key={tag}>
          {render_tags && <h3 style={tagStyle}>{tag}</h3>}
          <div style={gridStyle}>
            {groups[tag].map((page: IPage) => {
              return (
                <Page
                  key={page.path}
                  page={page}
                  theme={theme}
                  onClick={this.handlePageClick}
                />
              );
            })}
          </div>
        </Fragment>
      );
    });
  };
}

export default withStreamlitConnection(Grid);
