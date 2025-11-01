<?php

namespace App\Http\Resources\V1;

use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\JsonResource;

class ItemUsageResource extends JsonResource
{
    /**
     * Transform the resource into an array.
     *
     * @return array<string, mixed>
     */
    public function toArray(Request $request): array
    {
        return [
            'id' => $this->id,
            'item_id' => $this->item_id,
            'period' => $this->period,
            'usage' => $this->usage,
            'stock_start' => $this->stock_start,
            'stock_end' => $this->stock_end,
            'restocked' => $this->restocked,
            'restock_qty' => $this->restock_qty,
            'item' => $this->whenLoaded('item', function () {
                return [
                    'id' => $this->item->id,
                    'unit' => $this->item->unit,
                    'description' => $this->item->description,
                ];
            }),
            'created_at' => $this->created_at?->toISOString(),
            'updated_at' => $this->updated_at?->toISOString(),
        ];
    }
}
