import "@testing-library/jest-dom/vitest";
import { cleanup } from "@testing-library/react";
import { afterEach } from "vitest";

// Unmount components after each test so tests don't see each other's leftovers.
afterEach(cleanup);