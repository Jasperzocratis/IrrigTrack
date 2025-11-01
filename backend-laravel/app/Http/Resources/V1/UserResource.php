<?php

namespace App\Http\Resources\V1;

use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\JsonResource;

class UserResource extends JsonResource
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
            'fullname' => $this->fullname,
            'username' => $this->username,
            'email' => $this->email,
            'role' => $this->role,
            'image' => asset('storage/' . $this->image) ?? null,
            'location' => $this->location ? $this->location->location : null,
            'password' =>  $this->password,
            'created_at' => $this->created_at ? $this->created_at->toISOString() : null
        ];
    }
}
