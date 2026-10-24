import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it, vi } from "vitest";
import SearchBar, { EMPTY_FILTERS } from "./SearchBar";

describe("SearchBar", () => {
  it("sends the typed filters when Search is clicked", async () => {
    const onSearch = vi.fn();
    render(<SearchBar onSearch={onSearch} />);

    await userEvent.type(screen.getByLabelText("Make"), "Toyota");
    await userEvent.type(screen.getByLabelText("Max price"), "30000");
    await userEvent.click(screen.getByRole("button", { name: "Search" }));

    expect(onSearch).toHaveBeenCalledWith({ ...EMPTY_FILTERS, make: "Toyota", max_price: "30000" });
  });

  it("clears every filter when Clear is clicked", async () => {
    const onSearch = vi.fn();
    render(<SearchBar onSearch={onSearch} />);

    await userEvent.type(screen.getByLabelText("Make"), "Honda");
    await userEvent.click(screen.getByRole("button", { name: "Clear" }));

    expect(screen.getByLabelText("Make")).toHaveValue("");
    expect(onSearch).toHaveBeenCalledWith(EMPTY_FILTERS);
  });
});