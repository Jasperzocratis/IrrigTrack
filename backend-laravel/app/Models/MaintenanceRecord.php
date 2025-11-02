<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class MaintenanceRecord extends Model
{
    use HasFactory;

    protected $fillable = [
        'item_id',
        'maintenance_date',
        'reason',
        'condition_before_id',
        'condition_after_id',
        'technician_notes'
    ];

    protected $casts = [
        'maintenance_date' => 'date',
    ];

    public function item()
    {
        return $this->belongsTo(Item::class, 'item_id', 'id');
    }

    public function conditionBefore()
    {
        return $this->belongsTo(Condition::class, 'condition_before_id', 'id');
    }

    public function conditionAfter()
    {
        return $this->belongsTo(Condition::class, 'condition_after_id', 'id');
    }
}
