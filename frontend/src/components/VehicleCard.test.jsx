import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it, vi } from "vitest";
import VehicleCard from "./VehicleCard";

const car = { id: 1, make: "Toyota", model: "Corolla", category: "Sedan", price: 20000, quantity: 2 };
const noop = () => {};

function renderCard(props = {}) {
  return render(
    <VehicleCard vehicle={car} isAdmin={false} onPurchase={noop} onEdit={noop} onDelete={noop} onRestock={noop} {...props} />
  );
}

describe("VehicleCard", () => {
  it("shows the vehicle details", () => {
    renderCard();
    expect(screen.getByText("Corolla")).toBeInTheDocument();
    expect(screen.getByText("2 in stock")).toBeInTheDocument();
  });

  it("calls onPurchase when Purchase is clicked", async () => {
    const onPurchase = vi.fn();
    renderCard({ onPurchase });
    await userEvent.click(screen.getByRole("button", { name: "Purchase" }));
    expect(onPurchase).toHaveBeenCalledWith(car);
  });

  it("disables the purchase button when quantity is zero", () => {
    renderCard({ vehicle: { ...car, quantity: 0 } });
    expect(screen.getByRole("button", { name: "Sold out" })).toBeDisabled();
  });

  it("hides admin controls from regular users", () => {
    renderCard();
    expect(screen.queryByRole("button", { name: "Delete" })).not.toBeInTheDocument();
  });

  it("shows edit, restock and delete to admins", () => {
    renderCard({ isAdmin: true });
    for (const name of ["Edit", "Restock", "Delete"]) {
      expect(screen.getByRole("button", { name })).toBeInTheDocument();
    }
  });
});