declare module "react" {
  export function useEffect(
    effect: () => void | (() => void),
    dependencies?: readonly unknown[],
  ): void;

  export function useState<State>(
    initialState: State | (() => State),
  ): [State, (value: State | ((previousState: State) => State)) => void];
}

declare module "react/jsx-runtime" {
  export const Fragment: symbol;
  export function jsx(
    type: unknown,
    props: Record<string, unknown> | null,
    key?: string,
  ): JSX.Element;
  export function jsxs(
    type: unknown,
    props: Record<string, unknown> | null,
    key?: string,
  ): JSX.Element;
}

declare module "*.css" {
  const classes: Record<string, string>;
  export default classes;
}

declare namespace JSX {
  interface Element {}

  interface IntrinsicElements {
    [elementName: string]: Record<string, unknown>;
  }
}
