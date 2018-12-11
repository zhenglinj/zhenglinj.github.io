#include <string>
#include <iostream>
#include <map>

struct ClassInfo;

class DynBase
{
  public:
    DynBase() {};
    virtual ~DynBase() {};

  public:
    static bool Register(ClassInfo* classInfo);
    static DynBase* CreateObject(std::string type);
    virtual void Operation() = 0;

  private:
    static std::map<std::string, ClassInfo*> m_classInfoMap;
};

struct ClassInfo
{
    typedef DynBase* (*funCreateObject)(std::string);
    std::string Type;
    funCreateObject Fun;
    ClassInfo(std::string type, funCreateObject fun)
    {
        Type = type;
        Fun = fun;
        DynBase::Register(this);
    }
};

std::map<std::string, ClassInfo*> DynBase::m_classInfoMap =
        std::map<std::string, ClassInfo*>();

bool DynBase::Register(ClassInfo* classInfo)
{
    m_classInfoMap[classInfo->Type] = classInfo;
    return true;
}

DynBase* DynBase::CreateObject(std::string type)
{
    if (m_classInfoMap[type] != NULL)
    {
        return m_classInfoMap[type]->Fun(type);
    }
    return NULL;
}

class CIndustryOperate : public DynBase
{
  public:
    CIndustryOperate() {};
    virtual ~CIndustryOperate() {};
    void Operation() { std::cout << "IndustryOperate" << std::endl; };

  private:
    static DynBase* CreateObject() { return new CIndustryOperate(); }

  private:
    static ClassInfo* m_cInfo;
};

ClassInfo* CIndustryOperate::m_cInfo =
        new ClassInfo("IndustryOperate", (ClassInfo::funCreateObject)(CIndustryOperate::CreateObject));

int main(int argc, char *argv[])
{
    DynBase* p = DynBase::CreateObject("IndustryOperate");
    p->Operation();

    return 0;
}
