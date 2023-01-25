from OSRSBytes import *

def test(verbose = False):
    items = Items()
    test_item = ["rune dagger",1213]
    failed_list = []

    # getItem Method Test
    try:
        items.getItem(test_item[0])
        getItem_test = "Passed"
    except:
        getItem_test = "Failed"
        failed_list.append("getItem")

    # getName Method Test
    try:
        name = items.getName(test_item[1])
        if name == test_item[0]:
            getName_test = "Passed"
        else:
            getName_test = "Failed"
    except:
        getName_test = "Failed"
        failed_list.append("getName")

    # getItemID Method Test
    try:
        item_id = items.getItemID(test_item[0])
        if item_id == test_item[1]:
            getItemID_test = "Passed"
        else:
            getItemID_test = "Failed"
    except:
        getItemID_test = "Failed"
        failed_list.append("getItemID")

    # getBuyAverage Method Test
    try:
        getBuyAverage_test = "Passed"
        if not items.getBuyAverage(test_item[0]):
            getBuyAverage_test = "Failed"
            failed_list.append("getBuyAverage")
    except:
        getBuyAverage_test = "Failed"
        failed_list.append("getBuyAverage")

    # getSellAverage Method Test
    try:
        getSellAverage_test = "Passed"
        if not items.getSellAverage(test_item[0]):
            getSellAverage_test = "Failed"
            failed_list.append("getSellAverage")
    except:
        getSellAverage_test = "Failed"
        failed_list.append("getSellAverage")

    # getBuyQuantity Method Test
    try:
        getBuyQuantity_test = "Passed"
        if not items.getBuyQuantity(test_item[0]):
            getBuyQuantity_test = "Failed"
            failed_list.append("getBuyQuantity")
    except:
        getBuyQuantity_test = "Failed"
        failed_list.append("getBuyQuantity")    

    # getSellQuantity Method Test
    try:
        getSellQuantity_test = "Passed"
        if not items.getSellQuantity(test_item[0]):
            getSellQuantity_test = "Failed"
            failed_list.append("getSellQuantity")
    except:
        getSellQuantity_test = "Failed"
        failed_list.append("getSellQuantity")    

    # getBuyLimit Method Test
    try:
        getBuyLimit_test = "Passed"
        if not items.getBuyLimit(test_item[0]):
            getBuyLimit_test = "Failed"
            failed_list.append("getBuyLimit")
    except:
        getBuyLimit_test = "Failed"
        failed_list.append("getBuyLimit")

    # getShopPrice Method Test
    try:
        getShopPrice_test = "Passed"
        if not items.getShopPrice(test_item[0]):
            getShopPrice_test = "Failed"
            failed_list.append("getShopPrice")
    except:
        getShopPrice_test = "Failed"
        failed_list.append("getShopPrice")

    # getLowAlchValue Method Test
    try:
        getLowAlchValue_test = "Passed"
        if not items.getLowAlchValue(test_item[0]):
            getLowAlchValue_test = "Failed"
            failed_list.append("getLowAlchValue")
    except:
        getLowAlchValue_test = "Failed"
        failed_list.append("getLowAlchValue")

    # getHighAlchValue Method Test
    try:
        getHighAlchValue_test = "Passed"
        if not items.getHighAlchValue(test_item[0]):
            getHighAlchValue_test = "Failed"
            failed_list.append("getHighAlchValue")
    except:
        getHighAlchValue_test = "Failed"
        failed_list.append("getHighAlchValue")

    # isMembers Method Test
    try:
        isMembers_test = "Passed"
        if items.isMembers(test_item[0]) != False:
            isMembers_test = "Failed"
            failed_list.append("isMembers")
    except:
        isMembers_test = "Failed"
        failed_list.append("isMembers")

    # update Method Test
    try:
        update_test = "Passed"
        items.update()
        items.getName(test_item[1]) # Lets get some info
    except:
        update_test = "Failed"
        failed_list.append("update")

    if (verbose):
        print("getItem Test: {}".format(getItem_test))
        print("getName Test: {}".format(getName_test))
        print("getItemID Test: {}".format(getItemID_test))
        print("getBuyAverage Test: {}".format(getBuyAverage_test))
        print("getSellAverage Test: {}".format(getSellAverage_test))
        print("getBuyQuantity Test: {}".format(getBuyQuantity_test))
        print("getSellQuantity Test: {}".format(getSellQuantity_test))
        print("getBuyLimit Test: {}".format(getBuyLimit_test))
        print("getShopPrice Test: {}".format(getShopPrice_test))
        print("getLowAlchValue Test: {}".format(getLowAlchValue_test))
        print("getHighAlchValue Test: {}".format(getHighAlchValue_test))
        print("isMembers Test: {}".format(isMembers_test))
        print("update Test: {}".format(update_test))

        # Additional Tests above this comment
        assert len(failed_list)==0
        print("\nNumber of Failed Tests: {}".format(len(failed_list)))
        if failed_list:
            print("\n\tFailed tests:")
            for fail in failed_list:
                print("\t\t{}".format(fail))

        if len(failed_list)==0:
            print("Test Passed!")
            return True
        return False
    else:
        if len(failed_list)==0:
            return True
        return False
