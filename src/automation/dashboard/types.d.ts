declare module "*.css";

declare module "react" {
  export type FC<P = Record<string, never>> = (props: P) => JSX.Element | null;

  export type SetStateAction<S> = S | ((previousState: S) => S);
  export type Dispatch<A> = (value: A) => void;

  export function useEffect(
    effect: () => void | (() => void),
    dependencies?: readonly unknown[],
  ): void;

  export function useState<S>(
    initialState: S | (() => S),
  ): [S, Dispatch<SetStateAction<S>>];

  const React: {
    createElement: (...arguments_: unknown[]) => JSX.Element;
  };

  export default React;
}

declare namespace JSX {
  interface Element {}

  interface IntrinsicElements {
    [elementName: string]: any;
  }
}
