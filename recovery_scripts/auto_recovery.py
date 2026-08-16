# recovery_scripts/auto_recovery.py

def trigger_recovery(fault_code):
    """
    এই ফাংশনটি AI মডেলের পাঠানো fault_code এর ওপর ভিত্তি করে 
    সঠিক রিকভারি অ্যাকশন নেবে। 
    """
    if fault_code == 1:
        # Congestion (1) হলে ট্রাফিক অন্য লাইনে পাঠিয়ে দেবে
        return "Executing Script: Rerouting Traffic to Backup Path..."
        
    elif fault_code == 2:
        # Node Down (2) হলে রাউটার বা সার্ভিস রিস্টার্ট করবে
        return "Executing Script: Remote Rebooting Downed Node..."
        
    elif fault_code == 3:
        # High CPU (3) হলে ভারী প্রসেসগুলো কিল করে দেবে
        return "Executing Script: Killing Zombie Processes to free CPU..."
        
    else:
        return "System Normal - No Action Required"