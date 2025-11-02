<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class Location extends Model
{
    /** @use HasFactory<\Database\Factories\LocationFactory> */
    use HasFactory;

    protected $fillable = ['location', 'personnel'];

    public function item()
    {
        return $this->hasMany(Item::class);
    }

    public function users()
    {
        return $this->hasMany(\App\Models\User::class);
    }
}
