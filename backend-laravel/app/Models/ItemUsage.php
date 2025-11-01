<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class ItemUsage extends Model
{
    /**
     * The table associated with the model.
     *
     * @var string
     */
    protected $table = 'supply_usages';

    /**
     * The attributes that are mass assignable.
     *
     * @var array<int, string>
     */
    protected $fillable = [
        'item_id',
        'period',
        'usage',
        'stock_start',
        'stock_end',
        'restocked',
        'restock_qty',
    ];

    /**
     * The attributes that should be cast.
     *
     * @var array<string, string>
     */
    protected $casts = [
        'usage' => 'integer',
        'stock_start' => 'integer',
        'stock_end' => 'integer',
        'restocked' => 'boolean',
        'restock_qty' => 'integer',
    ];

    /**
     * Boot the model.
     *
     * @return void
     */
    protected static function booted()
    {
        static::creating(function ($usage) {
            if (empty($usage->period)) {
                $usage->period = static::getCurrentPeriod();
            }
        });
    }

    /**
     * Get the current period based on today's date
     *
     * @return string e.g., "Q1 2025"
     */
    public static function getCurrentPeriod(): string
    {
        $month = now()->month;
        $year = now()->year;
        
        if ($month >= 1 && $month <= 3) {
            return "Q1 $year";
        } elseif ($month >= 4 && $month <= 6) {
            return "Q2 $year";
        } elseif ($month >= 7 && $month <= 9) {
            return "Q3 $year";
        } else {
            return "Q4 $year";
        }
    }

    /**
     * Get the item that owns this usage record.
     *
     * @return BelongsTo
     */
    public function item(): BelongsTo
    {
        return $this->belongsTo(Item::class);
    }
}
